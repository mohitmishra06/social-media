import { AfterContentInit, Component, OnInit } from '@angular/core';
import { Leftmenu } from "../../components/dashboard/leftmenu/leftmenu";
import { Rightmenu } from "../../components/dashboard/rightmenu/rightmenu";
import { Stories } from "../../components/dashboard/stories/stories";
import { Addpost } from "../../components/dashboard/addpost/addpost";
import { Feed } from "../../components/dashboard/feed/feed";
import { UserDataStore } from '../../services/userData/user-data-store';
import { environment } from '../../../environments/environment.development';
import { ActivatedRoute } from '@angular/router';
import { ApiCallingService } from '../../services/api/api-calling.service';
import { User } from '../../interface/user.interface';
import { Toastr } from '../../services/toastr/toastr';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
  imports: [Leftmenu, Rightmenu, Stories, Addpost, Feed]
})

export class Dashboard implements OnInit{
  currentUser:any;
  url:string = "";
  userData?:User;
  userFollowers?:any;
  
  constructor(
    private _userData:UserDataStore,
    private _route:ActivatedRoute,
    private _apiCall:ApiCallingService,
    private _tostr:Toastr
  ){}

  ngOnInit(): void {
    this.url = environment.IMG_BASEURL;

    this._userData.glbUserData.subscribe(val => {
      this.currentUser = val.user;

      // Now currentUser is definitely available
      this.getUser(this.currentUser);
    });
  }

  // Get user data
  getUser(userId:any){
    // Call api for the user details
    this._apiCall.getApi('posts/get-all-post-with-all-details/', {"id":userId}).subscribe({
      // next() method will be executed only when there will be no error.
      next: (response: any) => {
        if (response.status === true) {
          this.userData = response.data;
          // Maybe redirect or show an alert
        } else {
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.errors])
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }
  
}
