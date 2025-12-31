import {Component, OnInit } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faThumbsUp } from '@fortawesome/free-solid-svg-icons';
import { Leftmenu } from "../../components/dashboard/leftmenu/leftmenu";
import { Feed } from "../../components/dashboard/feed/feed";
import { Rightmenu } from "../../components/dashboard/rightmenu/rightmenu";
import { UserDataStore } from '../../services/userData/user-data-store';
import { ActivatedRoute } from '@angular/router';
import { ApiCallingService } from '../../services/api/api-calling.service';
import { environment } from '../../../environments/environment.development';
import { CommonModule } from '@angular/common';
import { User } from '../../interface/user.interface';
import { Toastr } from '../../services/toastr/toastr';
import { DataUpdate } from '../../services/userData/data-update';

@Component({
  selector: 'app-profile',
  imports: [CommonModule,FontAwesomeModule, Leftmenu, Feed, Rightmenu],
  templateUrl: './profile.html',
  styleUrl: './profile.css'
})
export class Profile implements OnInit{
  icon = { faThumbsUp };
  currentUser:any;
  userId:any;
  userData?:User;
  url:string="";
  isBlocked?:boolean=false;
  blockedMessage:string="";
  
  constructor(
    private _userData:UserDataStore,
    private _route:ActivatedRoute,
    private _apiCall:ApiCallingService,
    private _tostr:Toastr,
    private _refData:DataUpdate,
    private route: ActivatedRoute
  ){}

  ngOnInit(): void {
    // Profile id
    // this.userId = this._route.snapshot.paramMap.get('id');   // Same route execute the page data not change only url change

    // This use for change data with url
    this.route.paramMap.subscribe(params => {
      this.userId = params.get('id');
      if (this.userId) {
        this.getUser(this.userId);
      }
    });

    // Current user id
    this._userData.user$.subscribe(user => {
      if(user){
        this.currentUser = user.user;
      }
    });    
    
    // Img url
    this.url = environment.IMG_BASEURL;
    
    // Call the function to get user data
    this.getUser(this.userId);

    // Refresh page
    this._refData.data$.subscribe(() => this.getUser(this.userId));
  }

  // Get user data
  getUser(userId:any){
    // Call api for the user details
    this._apiCall.getApi('auth/profile/', {"id":userId}).subscribe({
      // next() method will be executed only when there will be no error.
      next: (response: any) => {
        if (response.status === true) {
          this.userData = response.data;          
        } else {
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.error]);
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }
}
