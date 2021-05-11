# Model UN Conference Helper
The Model UN Conference Helper is a Django-based web app that helps chairs tally speeches, track motions, and calculate individual delegates' tandings.
It was used during DartMUN 2021 on April 9-11 in the United Nations Environmental Programme (UNEP) via PythonAnywhere.
Each chair accessed the site from their own computer and used Zoom to share a part of the screen for the delegates and hide a part to do tallying behind the scenes.
The site is no longer active due to maintenance costs. This markdown file will describe each of the files briefly and also include how to login.

## User Tiers
1. Secretariat - can access all committees and have Django superuser status
2. Chair/Staff - can access everything in their committee
3. Delegate - can access their personal information

## Login Info
1. Go to http://127.0.0.1:8000/dartmun/
2. Click on the Login buttom
  - Secretariat and Dais (Staff)
    - Username: first name + last initial + class year (e.g. henryk23)
    - Password: dartmun2021 (can be changed by the user later)
  - Delegates
    - Username: committee acronym + country name + 1 or 2 (if double delegation committee) (e.g. unepfrance1)
    - Password: dartmun2021 (can be changed by the user later)

## Other Pages Accessible w/o Login
### Secretariat Page
This page includes a bio for each secretariat member (current design imports info through a csv file)

### About Committees Page
This page lists the committees offered by the conference. If a user clicks on one of the links, they will be taken to a page that summarizes the committee's info.
The page lists the committee's topics and chairs (directors and managers).

## Pages Accessible after Login
### Position Papers
#### Secretariat
Secretariats will first be directed to a page listing the committees like the about committees page.
The secretariat should select the committee that they wish to view.

#### Chairs
The left column lists each of the delegations in the committee.
The right column (blank at the start) will display a delegation's position paper information once selected. 
Once a delegation is selected, there will be a tab for each topic to enter scores for the corresponding topic's position paper. There is a dropdown rubric.
The chair can either update the score or mark the paper as late or missing to assign a zero. A paper marked late or missing can be reverted by updating the rubric.
The chair can also add additional comments as necessary.

#### Delegates
Delegates can view their scores and comments for their papers.

### Tallies, Grades, Attendance Pages
- See history of tallies, see grades, see attendance records
- Secretariats will be directed to select the committee they wish to view
- Details on grading in the last section
- Grades calculate each time we refresh the grades page (because of relative scoring)
  - Highest score: Best Delegate candidate
  - 2nd: Outstanding Delegate candidate
  - 3rd: Honorable Mention candidate
  - 4th: Verbal Commendation candidate

### Admin Page
- Secretariats will be directed to select the committee they wish to view
- Left Column: list of delegations in committee
- Right Column: delegate's summary report (blank at start) including the following
  - Attendance Records
  - Position Paper Scores and Feedback
  - Speeches Made
  - Motions Passed
  - Scores by Category
- Printing the admin page formats the page in a printer-friendly method.

### Settings Page
Change your name, email, and password

## Working Papers and Resolutions
The "Working Papers and Resolutions" page consists of two parts:
1. View Working Papers and Resolutions
A table lists each working paper and resolution.

2. Add Working Papers and Resolutions
- The "Add Working Paper" form includes a dropdown for the topic and checkbox selections for sponsors and signatories.
- The "Add Resolution" form includes a dropdown for the topic and checkbox selections for sponsors and signatories. It also contains rubric fields to score the resolution.
- Selecting a sponsor removes country from signatory list (and vice versa)
- The forms will reject submission if not enough submissions
- The "Score Participation" form lists each delegation on the left column and a dropdown on the right column.

### Introducing a Working Paper/Resolution on the My Committee Page
- On the "Add Motion" form, select either "Introduce a Working Paper" or "Introduce a Resolution."
- Depending on whether you select working papers or resolutions, you can select a working paper or resolution that was entered on the "Working Papers and Resolutions" page.
- Once you pass the motion, the Committee Status portion of the My Committee page displays the current working paper or resolution.

### Introducing an Amendment on the My Committee Page
- Once you have a resolution selected, you can add an amendment using the "Add Amendment" tab.
- Select the type, enter the clause number (e.g. 1-a-i), mark whether it is friendly or unfriendly, enter a score, and select the sponsor and signatories.

### Voting on a Resolution or Amendment
On the "Vote Reso/Amend" tab, either select "Resolution" or "Amendment." Then, enter the number of votes for, votes against, and votes abstaining.
The sum of the votes should add up to be less than or equal to the number of delegations present. 
Once the vote passes, the website will raise a Javascript alert congratulating the passed resolution.

## My Committee
### Page Structure
1. Committee Status (top)
  - Votes required for simple/supermajority
  - Current committee session, topic, and caucus
  - List of motions raised in order of precedence
  - List of speakers on the speaker's list
  - Stopwatch for showing delegate speech times
  
2. Behind-the-Scenes Tally Forms (bottom)
  - Add speech tally or speaker's list entry
  - Add motion entry (including divisibility check for moderated caucus duration and individual speaking time)
  - Tracking Attendance/Present and Voting
  - (if resolution or amendment selected) Vote on resolution or amendment

The Committee Status portion is shared with other delegates via Zoom, and the tally forms are not shared. 
If delegates login using their account, they will only see the Committee Status portion.

### Steps to Running the Committee
#### 1. Roll Call

Take attendance by calling each delegation's country and mark them as present, present and voting, or absent. Once you click submit, the site will save your input.
Once you submit the data, you will see an updated Committee Status.

#### 2. Open Debate

A delegation should raise a "motion to open debate." In the "Add Motion" form, select the delegation that raises that motion. 
The motion to open debate should be preselected. Then click one of two buttons:
- Passes Under Chair's Discretion passes the motion without a vote. Select this to skip the voting procedure.
- Submit to add the motion entry to the motion list. 
  - Once you add this motion, you will see a new tab among the tally forms to vote on the motion.
  - You will also see the motion in the motion list in the committee status portion of the page. Click on the motion entry bullet to remove it.
  - Once it becomes time to vote, click on the "Vote Motion" tab and enter the votes for and against.
  - The motion to vote on (based on order of precedence) will be preselected.
  - If the sum of the votes for and votes against exceeds the number of delegations present, the site will give you an alert and disable the submit buttons.
  
#### 3. Primary Speaker's List (PSL)

You will now be directed to a form that lets you add speakers to the Primary Speaker's List.
Add them one at a time and enter scores for each speech on the "Add Tally" tab. On the add tally tab, the first speaker on the list will be preselected.
If there are no speakers on the list, you can select the speaker directly from the "Add Tally" tab.
Enter a score for that speaker. You can leave the time and comment fields blank. Once you're ready to set the agenda, head over to the "Add Motion" tab.
The motion name will be preselected. Use the dropdown to select the topic that the delegation wishes to debate on first.

#### 4. Open Floor

Once you've set the agenda, you will be directed to the "Add Motion" form. You will now see a new button that says "Speaker's List." 
Click on this button to start a "Secondary Speaker's List (SSL, a.k.a. General Speaker's List or GSL). The procedure is very similar to the Primary Speaker's List.

#### 5. Motion to Move into a Moderated Caucus

In the "Add Motion" form, select "Move into a Moderated Caucus." 
Once you make this selection, the form will update to include fields for duration, speaking time, and purpose.
All fields must be filled in to submit the motion entry. 
There is an automatic divisibility check between the duration and speaking time per Model UN parliamentary procedure.
Once a delegation's motion to move into a moderated caucus passes, an alert will show asking whether the delegation would like to speak first or last. 
If the delegation chooses to speak first, the delegation will be preselected in the add tally form for the first speech. 
If the delegation chooses to speak last, the delegation will be preselected in the add tally form for the last speech.
Throughout the caucus, the Committee Status portion will display the number of speeches remaining in the caucus.

#### 6. Motion to Move into an Unmoderated Caucus

In the "Add Motion" form, select "Move into an Unmoderated Caucus." 
Once you make this selection, the form will update to include fields for duration. This field must be filled in to submit.
Once the motion passes, the end time will be displayed on the Committee Status portion.

#### That's all you need to know to run your committee!
