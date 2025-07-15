import { Component, Input, OnChanges } from '@angular/core';
import { Post } from "../post/post";
import { User } from '../../../interface/user.interface';
import { ApiCallingService } from '../../../services/api/api-calling.service';
import { Toastr } from '../../../services/toastr/toastr';

@Component({
  selector: 'app-feed',
  imports: [Post],
  templateUrl: './feed.html',
  styleUrl: './feed.css'
})
export class Feed implements OnChanges{
  @Input() userId?:any;
  userPosts:any;

  constructor(
    private _apiCall:ApiCallingService,
    private _tostr:Toastr,
  ){}

  // This life cycle hook run after that the parent ngOnInit method runs
  ngOnChanges(): void {
    this.loadUser();  // Call this instead of doing logic inline
  }

  // This function call for get user data.
  loadUser(): void {
    if (this.userId) {
      this.getUserDetails(this.userId);  // Your existing function
    } else {
      console.warn('User is not come');
    }
  }

  // FUNCTION FOR UPDATION
  // Fetch current user details
  getUserDetails(id:User){
    this._apiCall.getApi("posts/get-all-post-with-all-details/", { "id":id }).subscribe({
      next: (response: any) => {
        if (response.status === true) {
          this.userPosts = response.data;
          console.log(this.userPosts);
          
        } else {
          console.log(response.errors);
          
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.errors])
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }
}