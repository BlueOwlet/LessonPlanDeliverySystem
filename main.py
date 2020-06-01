from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import glob
import shutil
from os.path import expanduser
import tkinter as tk
from tkinter import filedialog
# If modifying these scopes, delete the file token.pickle.
SCOPES = [

        'https://www.googleapis.com/auth/spreadsheets.readonly',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.readonly',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive'

        ]
home = os.path.realpath(expanduser("~"))
# materialFolder=os.path.realpath(filedialog.askdirectory())
# googleFolder = os.path.realpath(filedialog.askdirectory())

materialFolder=os.path.realpath('C:\\Users\\KamiO\\Desktop\\IA\\Material\\PDFs')
googleFolder = os.path.realpath('C:\\Users\\KamiO\\Google Drive (interactemails@gmail.com)\\Classes')

def login():


    # creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json',SCOPES)
    # client = gspread.authorize(creds)


    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    # global creds
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    global service
    service = build('sheets', 'v4', credentials=creds)

def GettingData():
    # Call the Sheets API
    spreadsheet_id = '1gEsoxidCDUByobm0RU7nThlY_-EODVOTc2A6vT-8Sz8'
    sheet = service.spreadsheets()

    global teacher_data
    range='A:A'
    result = sheet.values().get(spreadsheetId=spreadsheet_id,range=range).execute()
    teachers = result.get('values', [])

    global group_data
    range='B:B'
    result = sheet.values().get(spreadsheetId=spreadsheet_id,range=range).execute()
    groups = result.get('values', [])

    global material_data
    range='C:C'
    result = sheet.values().get(spreadsheetId=spreadsheet_id,range=range).execute()
    material = result.get('values', [])


    material_data=[]
    for mat in material:
        if mat:
            material_data.append(mat[0])

    group_data=[]
    for group in groups:
        if group:
            group_data.append(group[0])

    teacher_data=[]
    for teacher in teachers:
        if teacher:
            teacher_data.append(teacher[0])

def UpdateLPs():
    files = glob.glob(os.path.realpath('Material/PDFs/*/*.pdf'))
    print('Files loaded')
    for group in group_data:
        print('')
        if 'IAG' in group:

            teacher = teacher_data[group_data.index(group)]

            material = material_data[group_data.index(group)]
            print('{} Found in GSheets'.format(group))
            print('Searching for Group Folder')
            teacher_folder = glob.glob(os.path.realpath(home+'/Google Drive (interactemails@gmail.com)/Classes/'+teacher))
            print(teacher_folder)
            if teacher_folder==[]:
                print('Teacher Folder not found')
                print('Creating Teacher AND Group Folders')
                os.mkdir(home+'/Google Drive (interactemails@gmail.com)/Classes/'+teacher)
                os.mkdir(os.path.realpath(home+'/Google Drive (interactemails@gmail.com)/Classes/'+teacher+'/'+group))
                print('Teacher AND Group Folders created Successfully')
            else:
                print('Teacher Folder Found at {}'.format(teacher_folder))
            group_folder = glob.glob(home+'/Google Drive (interactemails@gmail.com)/Classes/'+teacher+'/'+group+'*')
            if group_folder == []:
                print('Group Folder not Found')
                os.mkdir(home+'/Google Drive (interactemails@gmail.com)/Classes/'+teacher+'/'+group)
                print('Group Folder Created Successfully')
            else:
                print('Group Folder found at {}'.format(group_folder))

            material_file = glob.glob(home+'/Desktop/IA/Material/PDFs/*/'+material)
            if material_file==[]:
                print('Material File(s) not Found')
            else:
                print('Material Found at {}'.format(material_file))
                shutil.copy(os.path.abspath(material_file[0]),os.path.abspath(home+'/Google Drive (interactemails@gmail.com)/Classes/'+teacher+'/'+group+'/'))
                print('Successfully PERFORMED')

class Group:
    def __init__(self,group_data):
        self.teacher = group_data[0]
        self.group = group_data[1]
        self.material = group_data[2]

    def getDirs(self):
        self.materialFile = glob.glob(os.path.realpath(materialFolder+'/*/'+self.material))
        if self.materialFile == []:
            print('Material not found')
            self.materialFile = ''
        else:
            self.materialFile = self.materialFile[0]
            print('Material File Found')


        self.teacherFolder = glob.glob(os.path.realpath(googleFolder+'/'+self.teacher))
        if self.teacherFolder == []:
            os.mkdir(googleFolder+'/'+self.teacher)
            print('New Teacher Folder Created for: {}'.format(self.teacher))
            self.teacherFolder = glob.glob(os.path.realpath(googleFolder+'/'+self.teacher))[0]
        else:
            self.teacherFolder=self.teacherFolder[0]
            print('Teacher Folder Found')

        self.groupFolder = glob.glob(self.teacherFolder+'/'+self.group)
        if self.groupFolder == []:
            print(self.groupFolder)
            os.mkdir(self.teacherFolder+'/'+self.group)
            print('New Group Folder Created for: {}'.format(self.groupFolder))
            self.groupFolder = glob.glob(os.path.realpath(self.teacherFolder+'/'+self.group))[0]
        else:
            self.groupFolder = self.groupFolder[0]
            print('Group Folder Found')
    def moveMaterial(self):
        print(self.materialFile, self.groupFolder)
        shutil.copy(self.materialFile,self.groupFolder)

def testing():
    # Call the Sheets API
    spreadsheet_id = '1gEsoxidCDUByobm0RU7nThlY_-EODVOTc2A6vT-8Sz8'
    sheet = service.spreadsheets()
    global group_data
    range='A:C'
    result = sheet.values().get(spreadsheetId=spreadsheet_id,range=range).execute()
    groups_data = result.get('values', [])

    for group_data in groups_data:
        if group_data:
            # print(group_data[0])
            # print(group_data[1])
            # print(group_data[2])
            try:
                print('')
                group = Group(group_data)
                print('{} | {} | {}'.format(group.group,group.teacher,group.material))

                if 'IAG' in group.group:
                    group.getDirs()
                    print(group.teacherFolder)
                    print(group.groupFolder)
                    print(group.material)
                    print('Dirs handling Successful')
                    group.moveMaterial()
                    print('Copy Successful')
            except Exception as e:
                print('Error: {}'.format(e))


def main():
    login()

    print('Material Folder set to: {}'.format(materialFolder))
    print('Google Folder set to: {}'.format(googleFolder))
    testing()
    # GettingData()
    # UpdateLPs()


main()
