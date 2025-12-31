import { CommonModule } from '@angular/common';
import { Component, Input, OnInit } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faThumbsUp } from '@fortawesome/free-solid-svg-icons';
import { environment } from '../../../../../../environments/environment.development';
import { UserDataStore } from '../../../../../services/userData/user-data-store';
import { ApiCallingService } from '../../../../../services/api/api-calling.service';
import { Toastr } from '../../../../../services/toastr/toastr';
import { DataUpdate } from '../../../../../services/userData/data-update';

// add emoji
import { PickerModule } from "@ctrl/ngx-emoji-mart";
import { ViewChild, ElementRef } from '@angular/core';

@Component({
  selector: 'app-comments-list',
  imports: [CommonModule, FontAwesomeModule, PickerModule],
  templateUrl: './comments-list.html',
  styleUrl: './comments-list.css'
})
export class CommentsList implements OnInit{
  @Input() postId?:any;
  @Input() comments?:any;
  url:string = environment.IMG_BASEURL;
  currentUser:any;
  currentUserImg:any;
  showEmoji:boolean = false;

  icon = {faThumbsUp}

  constructor(
    private _userData:UserDataStore,
    private _apiCall:ApiCallingService,
    private _tostr:Toastr,
    private _refData:DataUpdate
  ){}

  ngOnInit(): void {
    this._userData.user$.subscribe(val => { 
      this.currentUser = val.user;
      this.currentUserImg = val.userImg;
    }); 
  }

  // This line cought the input element with this line
  @ViewChild('commentInput') commentInput!: ElementRef<HTMLInputElement>;

  // Emoji dilog box open and close
  toggleEmoji() {
    this.showEmoji = !this.showEmoji;
  }

  // When emoji is selecte this function will run
  addEmoji(event: any) {
    const input = this.commentInput.nativeElement;    // This get the input from html like document.querySelector()

    // This two line find cursor position start and end
    const start = input.selectionStart ?? 0;
    const end = input.selectionEnd ?? 0;

    // This divided the input in three part which is before the emoji and emoji after the emoji this three part
    input.value =
      input.value.substring(0, start) +
      event.emoji.native +
      input.value.substring(end);

    // cursor emoji ke baad set
    setTimeout(() => {
      input.selectionStart = input.selectionEnd =
        start + event.emoji.native.length;
    });

    this.showEmoji = false;
  }

  // Create comment
  comment(event: Event, postId: any) {
    // Get current commet
    const input = event.target as HTMLInputElement;
    const commentText = input.value.trim();
    
    let commentData = {
      "userId":this.currentUser,
      "postId":postId,
      "desc":commentText
    }
    
    // Call api for the user details
    this._apiCall.postApi('users/comments/', commentData).subscribe({
      // next() method will be executed only when there will be no error.
      next: (response: any) => {
        if (response.status === true) {
          // Maybe redirect or show an alert
          this._tostr.toasterStatus(["text-gray-500", response.msg]);
          
          // 🔥 TELL EVERYONE DATA IS UPDATED
          this._refData.notifyForNewData();
        } else {
          // Maybe redirect or show an alert
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.msg]);
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }

}
