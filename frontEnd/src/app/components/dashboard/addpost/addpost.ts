import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faCamera, faImage, faPenFancy, faPlay, faVideoCamera } from '@fortawesome/free-solid-svg-icons';
import { ApiCallingService } from '../../../services/api/api-calling.service';
import { Toastr } from '../../../services/toastr/toastr';
import { Post } from '../../../interface/post.interface';
import { UserDataStore } from '../../../services/userData/user-data-store';

@Component({
  selector: 'app-addpost',
  imports: [FormsModule, FontAwesomeModule, CommonModule],
  templateUrl: './addpost.html',
  styleUrl: './addpost.css'
})
export class Addpost implements OnInit {
  errorMessage:string = '';
  userId:string =''
  currentUserImg?:string;

  icon = { faPenFancy, faVideoCamera, faImage, faCamera, faPlay}

  constructor(private _apiCall:ApiCallingService, private _tostr:Toastr, private _userData:UserDataStore){}

  ngOnInit(): void {
    this._userData.glbUserData.subscribe(val => {
      this.userId = val.userId;
      this.currentUserImg = val.userImg
    })
  }

  creatPost(postForm:NgForm){// Creating data for comparison.
    let postData:Post = {
      userId:this.userId,
      desc:postForm.value.post!
    }
    
    // Call api for authorisation.
    this._apiCall.postApi('posts/', postData).subscribe({
      // next() method will be executed only when there will be no error.
      next :(response:any) => {
        // On success.
        if(response.status === false){
            this._tostr .toasterStatus(['text-red', response.msg]);
            return;
          }
          this._tostr.toasterStatus(['text-gray-500', response.msg]);
          return;
      }
    });   
  }
}
