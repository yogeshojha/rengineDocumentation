# Multiple Users, Roles and Permissions

Roles and Permissions! Begining reNgine 2.0, we've taken your web application reconnaissance to a whole new level of control and security. Now, you can assign distinct roles to your team members—Sys Admin, Penetration Tester, and Auditor—each with precisely defined permissions to tailor their access and actions within the reNgine ecosystem.

## Adding Multiple Users
You can add multiple users from **Admin Settings** menu.

!!! danger "Attention"
    Please note that, the admin settings menu is only accesible to Sys Admin or root user!


![](https://github.com/yogeshojha/rengine/assets/17223002/aad1ab8d-3256-41f5-916e-e9064a7bf826)

Click on **+ Add User**

![](https://github.com/yogeshojha/rengine/assets/17223002/cec733c7-4c65-4e94-b1c7-b195f1ebd074)

You can assign below mentioned roles.

## Available Roles

  - Sys Admin: Sys Admin is a super user that has permission to modify system and scan related configurations, scan engines, create new users, add new tools etc. Super user can initiate scans and subscans effortlessly.

  - Penetration Tester: Penetration Tester will be allowed to modify and initiate scans and subscans, add or update targets, etc. A penetration tester will not be allowed to modify system configurations. A penetration tester will also not be able to add or modify users.

  - Auditor: Auditor can only view and download the report. An auditor can not change any system or scan related configurations nor can initiate any scans or subscans.


## Disable Users

You can also disable users from Admin Settings page. On every user accounts, you will see an action button called **Disable User**, clicking on it will disable the user. A disabled user will not be able to access reNgine.


## Changing Password

A Sys Admin can only change the password for other users. It is possible to change the password from the actions menu on each user.


## Changing Roles

A Sys Admin can also upgrade or downgrade the roles for any users from the same actions menu.
