import { CommonModule } from '@angular/common';
import { Component, Input, OnInit } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faThumbsUp } from '@fortawesome/free-solid-svg-icons';
import { environment } from '../../../../../../environments/environment.development';
import { UserDataStore } from '../../../../../services/userData/user-data-store';
import { ApiCallingService } from '../../../../../services/api/api-calling.service';
import { Toastr } from '../../../../../services/toastr/toastr';

@Component({
  selector: 'app-comments-list',
  imports: [CommonModule, FontAwesomeModule],
  templateUrl: './comments-list.html',
  styleUrl: './comments-list.css'
})
export class CommentsList implements OnInit{
  @Input() postId?:any;
  @Input() comments?:any;
  url:string = environment.IMG_BASEURL;
  currentUser:any;
  currentUserImg:any;

  icon = {faThumbsUp}

  constructor(private _userData:UserDataStore, private _apiCall:ApiCallingService, private _tostr:Toastr){}

  ngOnInit(): void {
    this._userData.glbUserData.subscribe(val => { 
      this.currentUser = val.user;
      this.currentUserImg = val.userImg;
    }); 
  }

  comment(event: Event, postId: any) {
    // Get current commet
    const input = event.target as HTMLInputElement;
    const commentText = input.value.trim();
    
    let commentData = {
      "userId":this.currentUser,
      "postId":postId,
      "desc":commentText
    }
    
    // Call api for the user details
    this._apiCall.postApi('users/comments/', commentData).subscribe({
      // next() method will be executed only when there will be no error.
      next: (response: any) => {
        if (response.status === true) {
          // Maybe redirect or show an alert
          this._tostr.toasterStatus(["text-gray-500", response.msg])
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
