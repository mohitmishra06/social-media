import { Component, Input, OnInit } from '@angular/core';
import { ApiCallingService } from '../../../services/api/api-calling.service';
import { ActivatedRoute } from '@angular/router';
import { Toastr } from '../../../services/toastr/toastr';
import { CommonModule } from '@angular/common';
import { environment } from '../../../../environments/environment.development';

@Component({
  selector: 'app-user-media-card',
  imports: [CommonModule],
  templateUrl: './user-media-card.html',
  styleUrl: './user-media-card.css'
})
export class UserMediaCard implements OnInit{
  @Input() user:any;
  posts:any;
  url = environment.IMG_BASEURL;

  constructor(
    private _apiCall:ApiCallingService,
    private _route:ActivatedRoute,
    private _tostr:Toastr
  ){}

  ngOnInit(): void {
    // Get user posts
    this.getAllPost(this.user.id)
  }

  // Get user post
  getAllPost(id:string){
    this._apiCall.getApi("posts/", { "id":id }).subscribe({
      next: (response: any) => {
        if (response.status === true) {        
          this.posts = response.data;
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
