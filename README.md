# Python Programming for Mobile Robotics @ Metropolia
Course materials for [ondroid.org](https://ondroid.org)

## Description of Repository Structure

- **images** folder: Contains images for the course. Images can be organized in any structure within this folder. We suggest saving images in different folders for different modules.
- **lessons** folder: Contains lessons in Markdown (.md) format. Lessons can be organized in any structure within this folder. We suggest saving lessons in different folders for different modules.
- **course-info.json** file: Contains basic information about the course, such as the full course name, short name, description, workload, student requirements, and image links.
- **lessons-list.json** file: Contains a list modules with lessons:

### Structure of lessons-list.json
**lessons-list.json** contains list with modules.
Every module in the list has structure:

- *str_id*: unique string identifier for each module in the course.
- *name*: display name of the module on the course page.
- *description*: description of the module.
- *sn*: Serial number of the module in the course, **starting from 0**.
- *lessons*: list of the lessons in the module.

Every lessons has structure:
- *str_id*: Unique string identifier for each lesson in the course.
- *name*: Display name of the lesson on the course page.
- *url*: URL for the lesson's Markdown file.
- *sn*: Serial number of the lesson in the course, starting from 0.
- *description*: description of the lesson.

### Structure of course-info.json
Course info:

- *fullCourseName*: Full name of the course.
- *shortCourseName*: Short name of the course.
- *shortDescription*: A short description of the course, up to 160 characters.
- *fullDescription*: A full description of the course, around 500 characters.
- *imageSmall*: URL for the small image (approximately 640x360 px).
- *imageBig*: URL for the large image (approximately 1920x1080 px).
- *workload*: Estimated time required to complete the course.
- *programmingLanguage*: string identifyer of programming language used in course.
## Completion of the 21 core Moodle activities

The 18 activities marked `simulation-or-lab` accept a successful simulator or physical robot check. Both paths save course progress and send 100/100 through LTI AGS for the launched Moodle activity. Earlier simulator practice attempts do not retroactively receive grades; a new check is required.

Electric Motors (`electric_motors`), Introduction to Octoliner Sensor (`intro_to_octoliner`) and Adaptive Speed (`adaptive_speed`) retain `simulation-and-lab`: both targets are available, and successful physical verification is required for completion. The optional Sandbox and activities outside the selected 21 keep their existing rules.

Publish frontend/backend support for `simulation-or-lab` before updating this course or the shared simulator manifest. The physical checkers, reference motion, reset poses and HAMK policy are unchanged.
