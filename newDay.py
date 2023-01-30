from datetime import date
import datetime
from math import floor
from pathlib import Path
import os

class Utils:
    def __init__(self, sprintStart):
        self.firstSprint = sprintStart

    def GetCurrentSprint(self, today):
        diff = (today - self.firstSprint).days
        sprint_len = 14
        return floor((diff) / sprint_len)

    def GetTodaysDate(self):
        return date.today()

    def DateToString(self, myDate):
        return myDate.strftime('%Y-%m-%d')

    def DateToUsString(self, myDate):
        return myDate.strftime('%m/%d/%Y')

class Files:
    def __init__(self):
        pass

    def MakeDirectory(self, path):
        cleanDir = os.path.dirname(path)
        if not os.path.exists(cleanDir):
            print(f'Making path "{cleanDir}"')
            os.makedirs(cleanDir)

    def MakeFile(self, path, initialText=''):
        theFile = Path(path)

        self.MakeDirectory(path)
        with open(theFile, 'a+') as file:
            file.seek(0)
            contents = file.read()
            
            if len(contents) == 0:
                file.writelines(initialText)

    def GetRootPath(self, sprint):
        return f'./Sprints/{sprint}'
    
    def GetTodaysNotesPath(self, sprint, todayString):
        root = self.GetRootPath(sprint)
        return f'{root}/{todayString}.md'

    def GetSprintNotesPath(self, sprint):
        root = self.GetRootPath(sprint)
        return f'{root}/{sprint}.md'

    def GetFilesPath(self, sprint):
        root = self.GetRootPath(sprint)
        return f'{root}/files/'

    def OpenInCode(self, path):
        os.system(f'code {path}')
    
    def GetTemplateFromFile(self, filename):
        with open(filename) as file:
            text = file.readlines()
            return ''.join(text)


class MakeTheNotes:
    def __init__(self):
        self.files = Files()
        self.utils = Utils(datetime.date(2011, 8, 3))
        self.today = self.utils.GetTodaysDate()
        self.todayString = self.utils.DateToString(self.today)
        self.sprint = self.utils.GetCurrentSprint(self.today)

    def MakeTheThings(self):
        notesPath = self.files.GetTodaysNotesPath(self.sprint, self.todayString)
        sprintNotesPath = self.files.GetSprintNotesPath(self.sprint)
        initialSprintText = self.GetSprintInitialText(self.sprint)
        initialNotesText = self.GetNotesInitialText(self.today)
        filesPath = self.files.GetFilesPath(self.sprint)

        self.files.MakeFile(notesPath, initialNotesText)
        self.files.MakeFile(sprintNotesPath, initialSprintText)
        self.files.MakeDirectory(filesPath)

    def OpenTheThings(self):
        notesPath = self.files.GetTodaysNotesPath(self.sprint, self.todayString)
        sprintNotesPath = self.files.GetSprintNotesPath(self.sprint)

        self.files.OpenInCode(notesPath)
        self.files.OpenInCode(sprintNotesPath)
    
    def GetSprintInitialText(self, sprint):
        templateFilename = '__sprint__.md'
        templateText = self.files.GetTemplateFromFile(templateFilename)
        sprintStr = templateText.replace('<sprint>', str(sprint))

        return sprintStr

    def GetNotesInitialText(self, today):
        templateFilename = '__day__.md'
        templateText = self.files.GetTemplateFromFile(templateFilename)
        todayUsString = self.utils.DateToUsString(today)

        dayStr = templateText.replace('<day>', todayUsString)
        datedStr = dayStr.replace('<date>', today.strftime("%A"))

        returnString = datedStr
        return returnString

def DoTheThing():
    notes = MakeTheNotes()
    
    notes.MakeTheThings()
    notes.OpenTheThings()


if __name__ == "__main__":
    # Do the thing!
    DoTheThing();