import { Component, OnInit } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import { ApiCallingService } from '../../../services/api/api-calling.service';
import { Toastr } from '../../../services/toastr/toastr';
import { UserDataStore } from '../../../services/userData/user-data-store';
import { CommonModule } from '@angular/common';
import { environment } from '../../../../environments/environment.development';

@Component({
  selector: 'app-stories',
  imports: [FontAwesomeModule, CommonModule,],
  templateUrl: './stories.html',
  styleUrl: './stories.css'
})
export class Stories implements OnInit{
  icon = { faPlus }
  currentUser:any;
  currentUserImg:any;
  currentUserBNRImg:any;
  userStories?:any;
  url:string = environment.IMG_BASEURL;
  
  constructor(
    private _apiCall:ApiCallingService,
    private _tostr:Toastr,
    private _userData:UserDataStore
  ){}

  ngOnInit(): void {
    this._userData.glbUserData.subscribe(val => { 
      this.currentUser = val.user;
      this.currentUserImg = val.userImg
      this.currentUserBNRImg = val.userCover
      // Call function for get all user story
      this.getStories(this.currentUser);
    });
  }

  // Get all user story
  getStories(userId:any){
    // Call api for saving data
    this._apiCall.getApi("users/story/", {"userId":userId}).subscribe({
      next: (response: any) => {
        if (response.status === true) {
          // Get all stories
          this.userStories = response.data;          
        } else {          
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.msg])
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }

  // Create new story
  newStory(event:Event, userId:any){
    // For upload image using formdata() object.
    let formData = new FormData();
    // Get File data.
    const file = (event.target as HTMLInputElement)?.files?.[0];

    // If file come, assign it to formData
    if (file) {
      formData.append('userId', userId);                        // Add user ID
      formData.append('file', file);                    // Actual File object
    }

    // Call api for saving data
    this._apiCall.postApi("users/story/", formData).subscribe({
      next: (response: any) => {
        if (response.status === true) {
          // Maybe redirect or show an alert
          this._tostr.toasterStatus(["text-gray-500", response.msg])
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

  // Video play auto
  onLoadedMetadata(video: HTMLVideoElement) {
    video.muted = true;
    video.play()
      .then(() => console.log('Playback started'))
      .catch(err => console.warn('Playback error:', err));
  }
}
