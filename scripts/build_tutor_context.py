#!/usr/bin/env python3
"""Build dated lesson notes and the opt-in AI profile manifest from course sources."""
import argparse
import ast
import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPO = 'https://github.com/autolab-fi/Metropolia-Line-Python-Course'
RAW = 'https://raw.githubusercontent.com/autolab-fi/Metropolia-Line-Python-Course/main/'
START = '<!-- metropolia-guidance:start -->'
END = '<!-- metropolia-guidance:end -->'


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def guidance(note):
    lines = [START, '## Metropolia setup notes', '', '**Guidance updated: ' + note['guidanceUpdated'] + '.**']
    validation = note['physicalValidation']
    if validation['status'] == 'verified':
        lines += ['The reference run passed the physical checker on **' + validation['date'] + '** (run ' + str(validation['submissionId']) + ').']
        if validation.get('scope'):
            lines += [validation['scope']]
    else:
        lines += ['**Physical validation pending:** the current reference program has simulator coverage, but a successful run on the current physical setup has not yet been confirmed.']
    if note['parameters']:
        settings = ', '.join('`' + key + ' = ' + str(value) + '`' for key, value in note['parameters'].items())
        lines += ['', 'Starting settings for this exercise: ' + settings + '.',
                  'Sensitivity is the Octoliner setup value (0–255); the detection threshold is a separate value applied to analog readings. Facing forward, sensors 0–2 are on the right, 3–4 in the center, and 5–7 on the left.',
                  'These settings apply to the Metropolia robot and lighting at the validation date. Inspect the readings again after changes to lighting, sensor height, wiring, or the track; a passing simulation alone does not confirm hardware calibration.']
    if note.get('colorGuidance'):
        lines += ['', note['colorGuidance'], 'The simulator uses measured sample colors, but does not fully reproduce sensor illumination and tape overlap. Use physical observations to validate color thresholds.']
    lines += [END]
    return '\n'.join(lines)


def checker_details(source, task_id):
    tree = ast.parse(source)
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == task_id)
    constants = {}
    for node in ast.walk(function):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper():
                    try:
                        value = ast.literal_eval(node.value)
                        constants[target.id] = sorted(value) if isinstance(value, set) else value
                    except (ValueError, TypeError):
                        pass
    return ast.get_docstring(function) or '', constants


def build(check=False):
    lessons = [t for m in json.loads((ROOT/'lessons-list.json').read_text()) for t in m['lessons']]
    notes = json.loads((ROOT/'tutor/task-notes.json').read_text())['tasks']
    sim = json.loads((ROOT/'simulation/manifest.json').read_text())['tasks']
    metadata = json.loads((ROOT/'simulation/generated/task-metadata.json').read_text())['tasks']
    assert set(notes) == {t['str_id'] for t in lessons} == set(sim), 'Active task coverage differs'
    profiles = {}
    changed = []
    for lesson in lessons:
        key = lesson['str_id']; note = notes[key]
        path = ROOT / lesson['url'].split('/main/', 1)[1]
        old = path.read_text()
        block = guidance(note)
        if START in old:
            text = re.sub(re.escape(START) + r'.*?' + re.escape(END), lambda _: block, old, flags=re.S)
        else:
            # Keep YAML front matter first, then put calibration next to the lesson title.
            heading = re.search(r'^# .+$', old, flags=re.M)
            assert heading, key
            text = old[:heading.end()] + '\n\n' + block + '\n' + old[heading.end():]
        if text != old:
            changed.append(str(path.relative_to(ROOT)))
            if not check:
                path.write_text(text)
        reference = (ROOT/note['reference']).read_text()
        ast.parse(reference)
        meta = metadata[key]
        checker_path = meta['verificationFile']
        checker = (ROOT/checker_path).read_text()
        description, constants = checker_details(checker, key)
        summary = re.sub(r'\s+', ' ', re.sub(r'```.*?```', '', text, flags=re.S))[:2000]
        validation = note['physicalValidation']
        rules = {
            'physical_start': meta.get('physicalStart'),
            'physical_checker_constants': constants,
            'simulator_checks': sim[key].get('checks', []),
            'physical_validation': validation,
            'starting_parameters': note['parameters'],
            'execution_mode': lesson['executionMode'],
            'completion_requires': 'successful physical verification; simulation is practice',
            'simulator_limitations': 'Measured Metropolia RGB samples do not reproduce all illumination/tape overlap. Timed motor motion and reset behavior need physical validation.',
            'do_not_reveal': ['full reference solution', 'raw checker implementation', 'hidden test thresholds'],
        }
        if note.get('colorGuidance'):
            rules['published_color_guidance'] = note['colorGuidance']
        refs = {'context_manifest_schema': 1, 'course_repo_url': REPO, 'task_url': lesson['url'],
                'reference_url': RAW + note['reference'], 'guidance_updated': note['guidanceUpdated'],
                'source_sha256': {'lesson': digest(text), 'template': digest(lesson['template']),
                                  'reference': digest(reference), 'checker': digest(checker),
                                  'simulation': digest(json.dumps(sim[key], sort_keys=True))}}
        profiles[key] = {
            'assignment_full_text': text, 'assignment_summary': summary,
            'reference_solution_text': reference,
            'verification_summary': '\n'.join(filter(None, [description, 'Hardware evidence: ' + json.dumps(validation),
                'The physical and simulator checks are distinct; consult their labeled rules. Reset failures before student execution are infrastructure failures. Do not infer a student-code failure from reset or video delivery alone. Provide hints rather than a complete solution.'])),
            'verification_rules': rules, 'common_mistakes': note['commonMistakes'],
            'repo_refs': refs, 'checker_source_ref': RAW + checker_path,
        }
    output = ROOT/'tutor/generated/profiles.json'
    encoded = json.dumps({'schemaVersion': 1, 'courseRepoUrl': REPO, 'tasks': profiles}, indent=2, ensure_ascii=False) + '\n'
    if not output.exists() or output.read_text() != encoded:
        changed.append(str(output.relative_to(ROOT)))
        if not check:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(encoded)
    if check and changed:
        raise SystemExit('Stale generated content: ' + ', '.join(changed))
    print(f'{len(profiles)} profiles; {len(changed)} files ' + ('need updates' if check else 'updated'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    build(parser.parse_args().check)
