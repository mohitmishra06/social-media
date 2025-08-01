import { Component } from '@angular/core';
import { environment } from '../../../../../environments/environment.development';
import { ApiCallingService } from '../../../../services/api/api-calling.service';
import { ActivatedRoute } from '@angular/router';
import { Toastr } from '../../../../services/toastr/toastr';
import { UserDataStore } from '../../../../services/userData/user-data-store';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-friend-requests',
  imports: [CommonModule],
  templateUrl: './friend-requests.html',
  styleUrl: './friend-requests.css'
})
export class FriendRequests {
  allFriendRequests:any;
  url = environment.IMG_BASEURL;
  userId:any;
  isFriendRequestStatus:boolean = false;

  constructor(
    private _apiCall:ApiCallingService,
    private _route:ActivatedRoute,
    private _tostr:Toastr
  ){}

  ngOnInit(): void {
    // current user id
    this.userId = this._route.snapshot.paramMap.get('id')

    // Get friends request function calling
    this.getAllFriendRequests(this.userId);
  }

  // Get all friends requests
  getAllFriendRequests(id:string){
    this._apiCall.getApi("users/friend-requests/", {"id":id}).subscribe({
      next: (response: any) => {
        if (response.status === true) {        
          this.allFriendRequests = response.data;                    
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

  // Accept friend request
  acceptFriendRequest(id:string){
    this._apiCall.postApi("users/friend-requests/", {"id":id}).subscribe({
      next: (response: any) => {
        if (response.status === true) {        
          this.isFriendRequestStatus = response.data;
          this._tostr.toasterStatus(["text-gray-500", response.msg])
          
          // Maybe redirect or show an alert
        } else {
          this.isFriendRequestStatus = response.data;
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.error])
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }

  // Decline friend request
  declineFriendRequest(id:string){
    this._apiCall.deleteApi("users/friend-requests/", {"id":id}).subscribe({
      next: (response: any) => {
        if (response.status === true) {        
          this.isFriendRequestStatus = response.data;
          this._tostr.toasterStatus(["text-gray-500", response.msg])
        } else {
          this.isFriendRequestStatus = response.data;
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.error])
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }

  // Set the button as condition
  get requestStatus(): boolean {
    if (this.isFriendRequestStatus) {
      return true;
    } else {
      return this.isFriendRequestStatus;
    }
  }
}
