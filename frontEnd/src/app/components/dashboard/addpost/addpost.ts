import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, FormsModule, NgForm, ReactiveFormsModule, Validators } from '@angular/forms';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faCamera, faImage, faPenFancy, faPlay, faVideoCamera } from '@fortawesome/free-solid-svg-icons';
import { ApiCallingService } from '../../../services/api/api-calling.service';
import { Toastr } from '../../../services/toastr/toastr';
import { Post } from '../../../interface/post.interface';
import { UserDataStore } from '../../../services/userData/user-data-store';

@Component({
  selector: 'app-addpost',
  imports: [FormsModule, FontAwesomeModule, CommonModule, ReactiveFormsModule],
  templateUrl: './addpost.html',
  styleUrl: './addpost.css'
})
export class Addpost implements OnInit {
  errorMessage:string = '';
  userId:string =''
  currentUserImg?:string;

  // For upload image using formdata() object.
  postForm: FormGroup;
  selectedFile: File | null = null;

  icon = { faPenFancy, faVideoCamera, faImage, faCamera, faPlay}

  constructor(
      private _apiCall:ApiCallingService,
      private _tostr:Toastr,
      private _userData:UserDataStore,
      private _fb:FormBuilder
    ){

     this.postForm = this._fb.group({
      description: new FormControl('', Validators.compose([Validators.required]))
    });
  }

  ngOnInit(): void {
    this._userData.glbUserData.subscribe(val => {
      this.userId = val.userId;
      this.currentUserImg = val.userImg
    })
  }

  // Update variable with select file
  onFileSelected(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (file) {
      this.selectedFile = file;
    }
  }

  creatPost(){
    // Create new post.
    const formData = new FormData();
    formData.append('userId', this.userId);
    formData.append('description', this.postForm.get('description')?.value);

    // If file is selected
    if (this.selectedFile) {
      formData.append('file', this.selectedFile);
    }
    
    // Call api for authorisation.
    this._apiCall.postApi('posts/', formData).subscribe({
      // next() method will be executed only when there will be no error.
      next :(response:any) => {
        // On success.
        if(response.status === false){
            this._tostr .toasterStatus(['text-[var(--btn-danger)]', response.errors]);
            return;
          }else {          
          this._tostr.toasterStatus(["text-gray-500", response.msg])
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }
}
