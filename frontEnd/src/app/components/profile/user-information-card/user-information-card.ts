import { CommonModule } from '@angular/common';
import { afterEveryRender, Component, Input, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { ApiCallingService } from '../../../services/api/api-calling.service';
import { ActivatedRoute } from '@angular/router';
import { Toastr } from '../../../services/toastr/toastr';
import { UserDataStore } from '../../../services/userData/user-data-store';
import { UpdateUser } from "../update-user/update-user";

@Component({
  selector: 'app-user-information-card',
  imports: [CommonModule, UpdateUser],
  templateUrl: './user-information-card.html',
  styleUrl: './user-information-card.css'
})
export class UserInformationCard implements OnInit{
  @Input() user:any;    // Data come from parent components
  isUserBlocked:boolean = false;
  isFollowing:boolean = false;
  isFollowingSent:boolean = false;
  userId:any;     // profile id
  currentUser:any;

  constructor(
    private _userData:UserDataStore,
    private _apiCall:ApiCallingService,
    private _tostr:Toastr
  ){}

  ngOnInit(): void {
    // Current user id
    this._userData.glbUserData.subscribe(val => { this.currentUser = val.user, this.userId = val.userId });

    // Call block user function
    this.followers(this.user.id);
    this.followerReqRes(this.user.id);
    this.blocked(this.user.id);    
  }

  // Get follower user details
  followers(id:any) {
    this._apiCall.getApi("users/followers/", { "id":id }).subscribe({
      next: (response: any) => {
        if (response.status === true) {
          this.isFollowing = response.data;
          // Maybe redirect or show an alert
        } else {
          console.log("User is not followers");
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }

  // Get follower Request and Response sent or not
  followerReqRes(id:any) {
    this._apiCall.getApi("users/requests/", { "id":id }).subscribe({
      next: (response: any) => {
        if (response.status === true) {
          this.isFollowingSent = response.data
          // Maybe redirect or show an alert
        } else {
          console.log("User is not request");
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }

  // Get block user details
  blocked(id:any) {
    this._apiCall.getApi("users/blocked/", { "id":id }).subscribe({
      next: (response: any) => {
        if (response.status === true) {
          this.isUserBlocked = response.data
          // Maybe redirect or show an alert
        } else {
          console.log("User is not blocked");
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }

  // Set the button as condition
  get followStatus(): string {
    if (this.isFollowing) {
      return 'Following';
    } else if (this.isFollowingSent) {
      return 'Request sent';
    } else {
      return 'Follow';
    }
  }

  // Set the button as condition
  get blockStatus(): string {
    if (this.isUserBlocked) {
      return 'Unblock User';
    } else {
      return 'Block User';
    }
  }

  // User follow or unfollow
  followUser(id:any){
    this._apiCall.deleteApi("users/followers/", { "id":id }).subscribe({
      next: (response: any) => {
        if (response.status === true) {        
          this.isFollowingSent = response.data;
          this._tostr.toasterStatus(["text-[var(--btn-success)]", response.msg])
          // Maybe redirect or show an alert
        } else {
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.error])
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }

  // User block or unblock
  blockUser(id:any){
    this._apiCall.deleteApi("users/blocked/", { "id":id }).subscribe({
      next: (response: any) => {
        if (response.status === true) {
          this.isUserBlocked = response.data;
          this._tostr.toasterStatus(["text-gray-500", response.msg])
          // Maybe redirect or show an alert
        } else {
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.error])
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }
}
