import { Component } from '@angular/core';
import { environment } from '../../../../../environments/environment.development';
import { ApiCallingService } from '../../../../services/api/api-calling.service';
import { ActivatedRoute } from '@angular/router';
import { Toastr } from '../../../../services/toastr/toastr';
import { UserDataStore } from '../../../../services/userData/user-data-store';

@Component({
  selector: 'app-friend-requests',
  imports: [],
  templateUrl: './friend-requests.html',
  styleUrl: './friend-requests.css'
})
export class FriendRequests {
  allRequests:any;
  url = environment.IMG_BASEURL;
  userId:any;

  constructor(
    private _apiCall:ApiCallingService,
    private _route:ActivatedRoute,
    private _tostr:Toastr
  ){}

  ngOnInit(): void {
    // current user id
    this.userId = this._route.snapshot.paramMap.get('id')

    // Get friends request function calling
    this.getAllRequests(this.userId);
  }

  // Get all friends requests
  getAllRequests(id:string){
    this._apiCall.getApi("users/friend-requests/", {"id":id}).subscribe({
      next: (response: any) => {
        if (response.status === true) {        
          this.allRequests = response.data;
          console.log(this.allRequests);
          
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
