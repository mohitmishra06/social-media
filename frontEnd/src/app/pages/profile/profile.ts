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
  ){}

  ngOnInit(): void {
    // Profile id
    this.userId = this._route.snapshot.paramMap.get('id')

    // Current user id
    this._userData.glbUserData.subscribe(val => this.currentUser = val.user)
    
    // Img url
    this.url = environment.IMG_BASEURL;

    // Call the function to get user data
    this.getUser(this.userId)
  }

  // Get user data
  getUser(userId:any){
    // Call api for the user details
    this._apiCall.getApi('auth/profile-details/', {"id":userId}).subscribe({
      // next() method will be executed only when there will be no error.
      next :(response:any) => {
        // On success.
        if(response.status === true){
            this.userData = response.data
            this.isBlocked = this.userData?.block;
            this.blockedMessage = response.msg            
            return;
          }
          return;
        }
    });
  }
}
