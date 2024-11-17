# Custom features for SGA.

## Grading for CCX coaches.

### Context

Out-of-the-box, SGA only allows the main-course admin users (instructors in the course access role model) to grade assignments.

This image shows the SGA view where course admins users can grade student submissions. As shown, the CCX coach cannot grade student submissions:

![](../docs/images/001-01.png "001-01")

This image shows the same SGA view, but with an admin role, indicating that only admin users of the course can grade student submissions:

![](../docs/images/001-02.png "001-02")

### Feature

This feature allows CCX coaches (ccx_coach in the course access role model) and CCX admin users (instructor in the course access role model) to grade assignments in their CCX courses.

![](../docs/videos/001-02.gif "001-01")

### Testing

- Install the plugin (LMS and CMS).
- Create a course and add an SGA component: https://github.com/Pearson-Advance/edx-sga/tree/pearson-release/olive.main#course-authoring-in-edx-studio
- Create a new CCX course.
- Submit a test assignment with a student user.
- Go to the unit containing the SGA component with the CCX tutor or instructor role.
- Click on the "Grade Submissions" button.
- Find the assignment and grade it.
- After grading the assignment, it should not be necessary to approve the grade.
- Go to the progress page, with the student user and check if the grade is assigned to the unit containing the SGA component.

## Custom Storage Backend

### Context

The SGA Xblock in its upstream repository approaches the storage capability by relaying on the Django's default storage
that is defined in the edx platform. There's also a feature where the storage backend to be used can be defined via
platform settings. For our fork, this feature adds the capability to define a site-aware backend via site configurations.

### Feature

To define a desired backend, follow the following format by defining the storage class and its kwargs.
As an example, below you will find the Site Configuration definition to use an AWS S3 bucket:

"SGA_STORAGE_SETTINGS": {
    "STORAGE_CLASS": "storages.backends.s3boto3.S3Boto3Storage",
    "STORAGE_KWARGS": {
        "access_key": "aws_access_key",
        "secret_key": "aws_secret_key",
        "bucket_name": "aws-bucket-name",
        "region_name": "us-east-1"
    }
}

Once it has been done, the SGA xblocks for the given site will manage the media objects with the defined storage backend.
If no settings are defined, the Xblock would use the default Django storage.
