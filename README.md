# ReadmeGenerator - Project Portfolio 3 - Python

## Introduction

<p align="center"><img src="static/images/IntroImage.png" width="50%" alt=""></p><br />



ReadmeGenerator is a tool that assists developers with the creation of README.md files for their projects. It is an interactive CLI than can be ran both locally and on Heroku. The tool guides you through the README.md creation process, and automatically creates and formats a markdown structured README.md file for you. 

The tool was created from my experience with projects to date, and the sometimes tediousness of formatting READMEs in markdown. I hope that this tool can help both myself and my classmates in the future.

You can view the live project here: <a href='https://readme-generator-ci.herokuapp.com/' target='_blank' rel='noopener'>ReadmeGenerator - Project Portfolio 3 - Python</a>

## User Experience

### Site Aims

 * To provide developers with a seamless experience when creating readme.md files. 
 * To allow developers to work on their readme files from any browser on any machine with their content saved in a worksheet.


### Target Audience

 * Developers
 * My classmates
 * Myself!


### User Stories

|   ID | GOAL                                                                                                              | ACTION                                                                        |
|------|-------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|
|    1 | Developers can manage the creation of readmes entirely within this tool.                                          | As a user, I can create a new readme project and have it saved online         |
|    2 | This allows developers to work on their readmes from different browsers or machines.                              | As a user, I can load a previously created readme project from a worksheet    |
|    3 | Developers can choose what sections to add to their readme so that the readme is custom to their needs            | As a user, I can add a new section to my readme                               |
|    4 | Developers can update their readme files as they progress through project development                             | As a user, I can modify sections that are already added to my readme          |
|    5 | Developers can preview what the file currently would look like with the data currently entered in markdown format | As a user, I can preview my readme file in the terminal                       |
|    6 | Developers can manage the entire creation of a readme file within this tool                                       | As a user, I can request that the tool creates a populated readme file for me |
|    7 | Developers can work on multiple projects in parallel without overwriting their other project readmes              | As a user, I can switch to a different readme project                         |

### Flowchart

<p align="center"><img src="static/images/ReadMeGeneratorFlowchart.png" width="50%" alt="ReadmeGenerator - Project Portfolio 3 - Python Flowchart"></p><br />



## Features

### Readme Project Creation:

 * When a project is created, a corresponding worksheet is created in Google Sheets
 * This allows developers to leave, and come back to their readme projects in the future if they wish

<p align="center"><img src="static/images/ProjectCreation.png" width="50%" alt=""></p><br />


### Loading of Readme Projects:

 * Developers can load their Readme Projects from any browser and continue working. 
 * This allows them to work on a variety of devices, including mobile devices.
 * Seperate worksheets are used to represent different projects

<p align="center"><img src="static/images/ProjectLoading.png" width="50%" alt=""></p><br />


### Storing of Readme Projects:

 * Storing data in google sheets allows developers to easily pick up where they left off with their work.
 * Records are stored with 3 columns; 'Section Type', 'Data Type', 'Value'
 * These columns help to indicate which sections and attributes that pieces of data correspond to.

<p align="center"><img src="static/images/ProjectStorage.png" width="50%" alt=""></p><br />


### Menu Helpers:

 * The menu_helpers.py file contains a set of functions that assist in the presenting of menus throughout the tool.
 * clear_screen() can clear the terminal window to reduce the amount of info on the screen at any one time
 * process_menu() shows the user various menu options that they can choose from, and ensures that appropriate input is given from the user.
 * The read_input() function (called by process_menu()) has the ability to read multiple lines of input before returning a response to the caller

<p align="center"><img src="static/images/MenuExample.png" width="50%" alt=""></p><br />


### Intro Section:

 * The IntroSection class allows developers to add an introduction to their project in their Readme.
 * It prompts the user to provide a description of their project (multi line input), a demo link for their project, along with an introductory image of the project.
 * Please see the Introduction section of this readme for reference of what is generated by the tool

<p align="center"><img src="" width="50%" alt=""></p><br />


### User Experience Section:

 * The UserExperienceSection class allows developers to outline what the intended experience users should have when using the project is.
 * This covers the subsections of 'Site Aims', 'Target Audience', 'User Stories', and a flowchart showing the flow of the tool usage. 

<p align="center"><img src="" width="50%" alt=""></p><br />


