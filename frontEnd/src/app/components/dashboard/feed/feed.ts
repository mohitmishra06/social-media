import { Component, HostListener, Input, OnChanges, OnInit } from '@angular/core';
import { Post } from "../post/post";
import { User } from '../../../interface/user.interface';
import { ApiCallingService } from '../../../services/api/api-calling.service';
import { Toastr } from '../../../services/toastr/toastr';
import { CommonModule } from '@angular/common';
import { UserDataStore } from '../../../services/userData/user-data-store';
import { DataUpdate } from '../../../services/userData/data-update';

@Component({
  selector: 'app-feed',
  imports: [Post, CommonModule],
  templateUrl: './feed.html',
  styleUrl: './feed.css'
})
export class Feed implements OnInit, OnChanges{
  @Input() userId?:any;   // If your comes from profile page this variable has a value
  @Input() moduleName?:any;
  followingUserPost:any;
  currentUser?:number;
  // Pagination variable scrolling
  page = 0;         // DRF offset based pagination, 0 se start
  limit = 5;
  loading = false;  // API call in progress
  hasMore = true;   // Are there more posts to load?
  userPosts: any[] = [];

  constructor(
    private _apiCall:ApiCallingService,
    private _tostr:Toastr,
    private _userData:UserDataStore,
    private _refData:DataUpdate
  ){}

  ngOnInit(): void {
    // Get current user
    this._userData.user$.subscribe(val => {
      if(!val) return;
      this.currentUser = val.user;
      this.userId ? '' : this.getFollowers(this.currentUser);
    });

    this.getUserDetails(null, this.moduleName);

     // 🔥 LISTEN FOR NEW POST EVENT
    this._refData.data$.subscribe(() => {
      this.reloadFeed();
    });
  }

  // This function reset all value for page reloading. but when we use page scrolling this will not work otherwise everything will wrong.
  resetFeed() {
    this.page = 0;
    this.hasMore = true;
    this.loading = false;
    this.userPosts = [];
  }

  // Call all user details and followers according to profile and dashboard
  reloadFeed(){
    this.resetFeed();   // ⭐ MOST IMPORTANT LINE, call reset function for reset everything
    
    if(this.moduleName === 'dashboard'){
      this.getUserDetails(null, this.moduleName);
      // this.getFollowers(this.currentUser);
    }

    if(this.userId){
      this.getUserDetails(this.userId, this.moduleName);
    }
  }
  
  // Find scroll position
  @HostListener('window:scroll', [])
  onScroll(): void {  // When scroll find end api will call
    if (this.loading || !this.hasMore) return;  // 🚨 Important check
    
    const scrollPosition = window.innerHeight + window.scrollY;
    const documentHeight = document.documentElement.scrollHeight;

    if (scrollPosition >= documentHeight - 200) {
      // this.getUserDetails(this.userId ?? null, this.moduleName);
      
      if(this.moduleName === 'dashboard'){
        this.getUserDetails(null, this.moduleName);
      }else{
        this.getFollowers(this.currentUser);
      }

      if(this.userId){
        this.getUserDetails(this.userId, this.moduleName);
      }
    }
  }

  // This life cycle hook run after that the parent ngOnInit method runs
  ngOnChanges(): void {    
    this.loadUser();  // Call this instead of doing logic inline
  }

  // This function call for get user data.
  loadUser(): void {
    if (this.userId) {
      this.getUserDetails(this.userId, this.moduleName);  // Your existing function
      // this.getFollowers(this.userId);
      this.getFollowers(this.currentUser);
    } else {
    // Call function
      console.log('User is not come');
    }
  }

  // FUNCTION FOR UPDATION
  // Fetch current user details
  getUserDetails(id:any=null, moduleName:any){
    if (this.loading || !this.hasMore) return;
    this.loading = true;
    
    // This is a query param
    const params = {
      id: this.userId || null,
      moduleName: this.moduleName,
      limit: this.limit.toString(),
      offset: (this.page * this.limit).toString()  // runtime offset
    };
    
    this._apiCall.getApi(
      "posts/get-all-post-with-all-details/",
      params).subscribe({
      next: (response: any) => {
        this.loading = false;   // After response come loading false
        if (response.results?.status === true) {
          // Append data in array for rendaring
          this.userPosts.push(...response.results?.data)
          // Next link exists -> more data
          this.hasMore = !!response.next; // This checks for next url came or not
          this.page++;    // Increse page number for offset
        } else {
          this.hasMore = false;   // When next url is not come.
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.errors])
        }
      },
      error: (err) => {
        this.loading = false;   // After response come loading false
        console.error("API call failed", err);
      }
    });
  }

  // Get user following data like post, comment, like etc.
  getFollowers(id:any){
    // Call api for the user details
    this._apiCall.getApi('users/get-all-followers/', {"id":id}).subscribe({
      // next() method will be executed only when there will be no error.
      next: (response: any) => {
        if (response?.status === true) {
          this.followingUserPost = response?.data;
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