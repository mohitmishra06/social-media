import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faComment, faPause, faPlay, faShare, faThumbsUp } from '@fortawesome/free-solid-svg-icons';
import { Comments } from "./comments/comments";
import { User } from '../../../interface/user.interface';
import { environment } from '../../../../environments/environment.development';
import { CommonModule } from '@angular/common';
import { PostIntractions } from "./post-intractions/post-intractions";
import { ApiCallingService } from '../../../services/api/api-calling.service';
import { Toastr } from '../../../services/toastr/toastr';
import { UserDataStore } from '../../../services/userData/user-data-store';
import { DataUpdate } from '../../../services/userData/data-update';

@Component({
  selector: 'app-post',
  imports: [FontAwesomeModule, Comments, CommonModule, PostIntractions],
  templateUrl: './post.html',
  styleUrl: './post.css'
})
export class Post implements OnInit{
  @Input() posts:any;
  @Input() moduleName:any;
  user?:any;
  userPosts?:any;
  likes?:any;
  comments?:number;
  url:string = environment.IMG_BASEURL;
  // This handle video time
  videoCurrentTime = 0;
  videoDuration = 0;

  icon = { faPlay, faPause }
  
  constructor(
    private _apiCall:ApiCallingService,
    private _tostr:Toastr,
    private _refData:DataUpdate
  ){}

  ngOnInit(): void {
    // Different for dashboard and profile
    if(this.moduleName=="profile"){ 
      this.user = this.posts.following;
      this.userPosts = this.posts.user_post;
    }else{
      this.user = this.posts.user; 
    }
    
    // Common for profile and dashboard
    this.likes = this.posts.post_like;
    this.comments = this.posts.post_comment;
  }

  // Play video only one at a time
  onVideoPlay(event: Event): void {
    const currentVideo = event.target as HTMLVideoElement;

    // Pause all other videos on the page
    const videos = document.querySelectorAll('video');
      videos.forEach((video) => {
        if (video !== currentVideo) {
          video.pause();
        }
      });
  }

  // Handle play/pause with one button click
  togglePlayPause(video: HTMLVideoElement): void {
    if (video.paused) {
      video.play();
    } else {
      video.pause();
    }
  }

  // This function manage the range input timing with the live video time  
  onTimeUpdate(video: HTMLVideoElement): void {
    this.videoCurrentTime = video.currentTime;
    this.videoDuration = video.duration;
  }

  onSeek(event: Event, video: HTMLVideoElement): void {
    const value = (event.target as HTMLInputElement).value;
    video.currentTime = +value;
  }

  // Delete post
  deletePost(userId:any, postId:any){    
    // Call api for saving data
    this._apiCall.deleteApi("posts/", {"userId":userId, "postId":postId}).subscribe({
      next: (response: any) => {
        if (response.status === true) {
          // Get all stories
          this._tostr.toasterStatus(["text-gray-500", response.msg])
          
          // 🔥 TELL EVERYONE DATA IS UPDATED
          this._refData.notifyForNewData();
        } else {
          console.log(response.errors);
          
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.errors])
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }
}
