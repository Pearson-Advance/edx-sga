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

## AWS S3 Storage feature

### Context

The SGA Xblock in its upstream repository approaches the storage capability by relaying on the Django's default storage
that is defined in the edx platform. This feature adds the capability to define whether to use the Django storage
(which is set by default and does not require configurations), or define a custom AWS S3 bucket to store the media
objects processed through the SGA Xblock. This feature is site-aware and could be define in the Admin portal of the
platform.

### Feature

Set the AWS S3 bucket to the Xblock through the Site configurations using the following format:

"aws_s3_storage_data": {
    "aws_s3_access_key": "yours_access_key",
    "aws_s3_secret_key": "yours_secret_key",
    "aws_s3_bucket_name": "AWS_s3_bucket_name",
    "aws_s3_region_name": "yours_aws_region_name"
}

Once it has been done, the SGA xblocks for the given site will manage the media objects with the AWS S3 bucket.
If no settings are defined, the Xblock would use the defrault Django storage.
