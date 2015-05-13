import urllib2
import os
import ast

null = None

if os.path.isfile('dlpath.txt'):
    f = open('dlpath.txt','r')
    dlpath = f.read()
    f.close()
else:
    print 'Welcome to [Py]SagaLoader. Please specify a download location for all future downloads.'
    dlpath = raw_input()
    f = open('dlpath.txt','w+')
    f.write(dlpath)
    f.close()

def main():
    musicName = raw_input('Enter track name: ')
    APIurl = 'http://rhythmsa.ga/api.php?api=everything&q='+musicName.replace(' ','+')
    APIQuery = urllib2.urlopen(APIurl)
    APIResponse = APIQuery.read()
    try:
        APIResponse = ast.literal_eval(APIResponse)
        print 'Your query was:', musicName,'\nIt returned the following result:-'
        print '\nTrack Name: '+ APIResponse['track'] + '\nAlbum: '+APIResponse['album']+'\nArtist: '+APIResponse['artist']+'\nGenre: '+ APIResponse['genre']
        choice = raw_input('Are you sure you want to download this track? Y/N ')
        if choice=='Y' or choice == 'y':
            trackURL = 'http://rhythmsa.ga/api.php?api=mp3_url&q='+musicName.replace(' ','+')
            MP3Query = urllib2.urlopen(trackURL)
            MP3URL = MP3Query.read()
            MP3 = urllib2.urlopen(MP3URL)
            print '\n***************** Downloading. Please wait. *****************\n'
            # TO ADD: Download progress. 
            MP3File = MP3.read()
            saveName = dlpath+APIResponse['artist']+'-'+APIResponse['track']+'.mp3'
            with open(saveName, 'wb') as file:
                file.write(MP3File)
            print 'Saved '+APIResponse['track'] +' at '+ saveName
        elif choice=='N' or choice == 'n':
            response = raw_input('Want to try again? Try rephrasing your query this time. Y/N')
            if response == 'Y' or response == 'y':
                main()
            elif response == 'N' or response == 'n':
                exit(0)
    except ValueError:
        print "Your query", musicName,"was invalid. Please try again."
        main()
if __name__ == '__main__':
    main()
