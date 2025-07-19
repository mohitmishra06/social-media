import { Component, Input, OnChanges, OnInit } from '@angular/core';
import { Post } from "../post/post";
import { User } from '../../../interface/user.interface';
import { ApiCallingService } from '../../../services/api/api-calling.service';
import { Toastr } from '../../../services/toastr/toastr';
import { CommonModule } from '@angular/common';
import { UserDataStore } from '../../../services/userData/user-data-store';

@Component({
  selector: 'app-feed',
  imports: [Post, CommonModule],
  templateUrl: './feed.html',
  styleUrl: './feed.css'
})
export class Feed implements OnInit, OnChanges{
  @Input() userId?:any;
  userPosts:any;
  followingUserPost:any;
  currentUser?:number;

  constructor(
    private _apiCall:ApiCallingService,
    private _tostr:Toastr,
    private _userData:UserDataStore
  ){}

  ngOnInit(): void {
    // Get current user
    this._userData.glbUserData.subscribe(val => { 
      this.currentUser = val.user
      this.userId ? '' : this.getFollowers(this.currentUser)
    } );
  }

  // This life cycle hook run after that the parent ngOnInit method runs
  ngOnChanges(): void {    
    this.loadUser();  // Call this instead of doing logic inline
  }

  // This function call for get user data.
  loadUser(): void {
    if (this.userId) {
      this.getUserDetails(this.userId);  // Your existing function
      this.getFollowers(this.userId);
    } else {
    // Call function
      console.log('User is not come');
    }
  }

  // FUNCTION FOR UPDATION
  // Fetch current user details
  getUserDetails(id:User){
    this._apiCall.getApi("posts/get-all-post-with-all-details/", { "id":id }).subscribe({
      next: (response: any) => {
        if (response.status === true) {
          this.userPosts = response.data;
        } else {
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.errors])
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }

  // Get user following data
  getFollowers(userId:any){
    // Call api for the user details
    this._apiCall.getApi('users/get-all-followers/', {"id":userId}).subscribe({
      // next() method will be executed only when there will be no error.
      next: (response: any) => {
        if (response.status === true) {
          this.followingUserPost = response.data;          
          // Maybe redirect or show an alert
        } else {
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.msg])
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }
}