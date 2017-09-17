# -*- coding: utf-8 -*-
"""
    SNAB
    ~~~~~~

    SimpleNote as Blog is an application for publishing 
    your SimpleNote notes as blog posts.

    :copyright: (c) 2017 by Artur Nebot.
    :license: BSD, see LICENSE for more details.
"""
import markdown
from MLStripper import MLStripper
from simplenote import Simplenote

from flask import Blueprint, request, session, g, redirect, url_for, abort, \
     render_template, flash, current_app

class SimplePost:
    PostKey=''
    PostTitle=''
    PostContent=''
    def __init__(self,PostTitle='',PostContent=''):
        self.PostTitle=PostTitle
        self.PostContent=PostContent

# create our blueprint :)
bp = Blueprint('snab', __name__)

def getSimpleNote():
    return Simplenote(current_app.config['SN_USER'],current_app.config['SN_PASSWORD'])

@bp.route('/')
def show_entries():
    s = getSimpleNote()
    (notes_key,result) = s.get_note_list(tags=current_app.config['SN_PUBLISH_TAGS'])
    if result == 0: # Success
        all_notes_content=[]
        print "Found ["+ str(len(notes_key)) + "] notes to publish..."
        for note in notes_key:
            (note_content,result) = s.get_note(note['key'])
            if result == 0:
                html_post_content = markdown.markdown(unicode(note_content['content'],"utf-8"))
                post_lines = html_post_content.splitlines()
                
                sp = SimplePost()
                sp.PostKey = note['key']

                striper = MLStripper()
                striper.feed(post_lines[0])
                sp.PostTitle =  striper.get_data()
                sp.PostContent = ''.join(post_lines[1])
                
                all_notes_content.append(sp)

        return render_template('show_entries.html',blogTitle = current_app.config['MAIN_TITLE'],entries = all_notes_content)

@bp.route('/<entry_key>')
def show_entry(entry_key):
    s = getSimpleNote()
    (note_content,result) = s.get_note(entry_key)
    if result == 0:
        sp = SimplePost()
        sp.PostContent = markdown.markdown(unicode(note_content['content'],"utf-8"))
        return render_template('show_entry.html',blogTitle=current_app.config['MAIN_TITLE'],entry = sp)