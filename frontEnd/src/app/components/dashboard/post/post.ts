import { Component, Input, OnInit } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faComment, faShare, faThumbsUp } from '@fortawesome/free-solid-svg-icons';
import { Comments } from "./comments/comments";
import { User } from '../../../interface/user.interface';
import { environment } from '../../../../environments/environment.development';
import { CommonModule } from '@angular/common';
import { PostIntractions } from "./post-intractions/post-intractions";

@Component({
  selector: 'app-post',
  imports: [FontAwesomeModule, Comments, CommonModule, PostIntractions],
  templateUrl: './post.html',
  styleUrl: './post.css'
})
export class Post implements OnInit{
  @Input() post:any;
  user?:User;
  userPosts?:any;
  likes?:any;
  comments?:number;
  url:string = environment.IMG_BASEURL;

  ngOnInit(): void {
    this.user = this.post.following;
    this.likes = this.post.user_like;
    this.comments = this.post.user_comment;
    this.userPosts = this.post.user_post
  }
}
