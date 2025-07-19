import { Component, Input, OnInit } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faThumbsUp } from '@fortawesome/free-solid-svg-icons';
import { ApiCallingService } from '../../../../services/api/api-calling.service';
import { Toastr } from '../../../../services/toastr/toastr';
import { CommentsList } from "./comments-list/comments-list";

@Component({
  selector: 'app-comments',
  imports: [FontAwesomeModule, CommentsList],
  templateUrl: './comments.html',
  styleUrl: './comments.css'
})
export class Comments implements OnInit {
  @Input() postId?:number;
  postComments?:string;

  icon = {faThumbsUp}

  constructor(private _apiCall:ApiCallingService, private _tostr:Toastr){}

  ngOnInit(): void {
    // Call function for getting all comments accourding to post
    this.getAllComments(this.postId);
  }

  getAllComments(postId?:number){
    // Call api for the user details
    this._apiCall.getApi('users/comments/', {"postId":postId}).subscribe({
      // next() method will be executed only when there will be no error.
      next: (response: any) => {
        if (response.status === true) {
          this.postComments = response.data;
          // Maybe redirect or show an alert
        } else {
          // Maybe redirect or show an alert
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }
}