import { CommonModule } from '@angular/common';
import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faComment, faShare, faThumbsUp } from '@fortawesome/free-solid-svg-icons';
import { UserDataStore } from '../../../../services/userData/user-data-store';
import { ApiCallingService } from '../../../../services/api/api-calling.service';
import { Toastr } from '../../../../services/toastr/toastr';

@Component({
  selector: 'app-post-intractions',
  imports: [CommonModule, FontAwesomeModule],
  templateUrl: './post-intractions.html',
  styleUrl: './post-intractions.css'
})
export class PostIntractions implements OnInit {
  // Props variable
  @Input() postId?:any;
  @Input() likes?:any;
  @Input() comments?:any;

  // Developer variable
  userLikes?:number[] = [];
  userComments?: number[] = [];
  currentUser:any;
  isUserLike:boolean = false;
  isUserComment:boolean = false;

  icon={faThumbsUp, faComment, faShare}

  constructor(private _userData:UserDataStore, private _apiCall: ApiCallingService, private _tostr:Toastr){}

  ngOnInit(): void {
    // Get current user
    this._userData.glbUserData.subscribe(val => { this.currentUser = val.user } );

    // Count likes
    for(let i = 0; i< this.likes.length; i++){
      if(this.postId == this.likes[i].post){
        this.userLikes?.push(this.postId);        
      }

      if(this.postId == this.likes[i].post && this.currentUser == this.likes[i].user){
        this.isUserLike=true;
      }
    }

    // Count comments
    for(let i = 0; i< this.comments.length; i++){
      if(this.postId == this.comments[i].post){
        this.userComments?.push(this.postId)
      }

      if(this.postId == this.comments[i].post && this.currentUser == this.comments[i].user){
        this.isUserComment=true;
      }
    }
  }

  // POST COMMENT AND LIKE FUNCTION
  postLike(userId:number, postId:number){
    // Call api for the user details
    this._apiCall.getApi('users/likes/', {"userId":userId, "postId":postId}).subscribe({
      // next() method will be executed only when there will be no error.
      next: (response: any) => {
        if (response.status === true) {
          this.isUserLike = response.data;
          // Maybe redirect or show an alert
          this._tostr.toasterStatus(["text-gray-500", response.msg]);
        } else {
          // Maybe redirect or show an alert
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.msg]);
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }

}
