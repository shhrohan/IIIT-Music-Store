# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    
    message = 'Wel-Come To IIIT Music Store !!'
    
    if(auth.is_logged_in()):
        
        id = auth.user_id
        row=db(db.playlist.user_id==id).select().first()
        query1 = ((db.playlist.shared == 2)|(db.playlist.shared == 1))
        query2 = (db.playlist.user_id != auth.user_id )
        public_playlists=db(query1 & query2).select()
        
        if (str(row)=="None"):
         try:
            row_a = db(db.playlist.user_id==request.args[0]).select().first()
            songIds=row_a.songlist.split(",")
            songs = []
            playlistName = row_a.name
            songlist = row_a.songlist
            for id in songIds:
                songs.append(db(db.song.id==id).select().first())
                
            return dict(message=message,playlist_exist='true',isloggedin='true',songs=songs,public_playlists=public_playlists,playlistName=playlistName,visitor=1,songlist=songlist)
         
         except IndexError:
             return dict(message=message,isloggedin='true',public_playlists=public_playlists)
         pass
         
        else:
            try:
                
                row_a = db(db.playlist.user_id==request.args[0]).select().first()
                songIds=row_a.songlist.split(",")
                songs = []
                playlistName = row_a.name
                songlist = row_a.songlist
                for id in songIds:
                    songs.append(db(db.song.id==id).select().first())
                    
                pass
                
                return dict(message=message,isloggedin='true', playlist_exist='true',songs=songs, playlistName=playlistName,visitor=1,public_playlists=public_playlists,songlist=songlist)
                
            except IndexError:
                
                songIds=row.songlist.split(",")
                songs = [];
                playlistName = row.name
                for id in songIds:
                    songs.append(db(db.song.id==id).select().first())
                pass  
                songlist = row.songlist
                
                return dict(message=message ,isloggedin='true', playlist_exist='true', songs=songs, playlistName=playlistName,public_playlists= public_playlists,songlist=songlist)
            pass
    else:
           try :
                row = db(db.playlist.user_id==request.args[0]).select().first()
                songIds=row.songlist.split(",")
                songs = []
                playlistName = row.name
                songlist = row.songlist
                
                for id in songIds:
                    songs.append(db(db.song.id==id).select().first())
                pass
                
                return dict(message=message,isloggedin='true', playlist_exist='true', songs=songs, playlistName = playlistName, visitor=1 , public_playlists=db(db.playlist.shared==2).select(),songlist=songlist)
           except IndexError:
                return dict(message=message,public_playlists= db(db.playlist.shared==2).select())
           pass
    pass
    
def playlist():
    message=T('Wel-Come To IIIT Music Store !!');
    if(auth.is_logged_in()):
        user_id = auth.user_id
        row=db(db.playlist.user_id == user_id).select().first()    
        if (str(row)!="None"):
            songs = []
            p_songs = []
            all_songs = db(db.song).select()  
            playlist_name = row.name      
            songIds = row.songlist.split(",")
            for song in all_songs:
                if str(song['id']) not in songIds:
                        songs.append(song)
                pass
            pass
            for id in songIds:
                p_songs.append(db(db.song.id==id).select().first())
            pass 
            
            shared=row.shared
            
            return dict(shared=shared,title="Edit Playlist",playlist_name=playlist_name,songlist=','.join(songIds),message=message,isloggedin='true',songs = db(db.song).select(),p_songs = p_songs)
        else:
            return dict(shared=0,title="Create Playlist",message=message,isloggedin='true',songs=db(db.song).select())
        pass
    else:
      redirect(URL('index'))

def save():
    user_id = auth.user_id
    songlist = request.vars.songlist
    shared = request.vars.shared
    
    row=db(db.playlist.user_id == user_id).select().first()   
     
    if (str(row)!="None"):
        row.update_record(songlist=songlist,name=request.vars.playlist_name,shared=shared)
        response.flash = T("Playlist updated succesfully!!")
    else:
        id = db.playlist.insert(user_id=user_id,songlist=songlist,name=request.vars.playlist_name)
        if(id!=-1):
            response.flash = T("Playlist created succesfully!!")
        else:
            response.flash = T("Error occured. PLease login again !!")
        pass
    pass
    
    redirect(URL('index'))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
