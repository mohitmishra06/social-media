import { Component, OnInit } from '@angular/core';
import { UserDataStore } from '../../../../services/userData/user-data-store';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-profile-card',
  imports: [RouterModule],
  templateUrl: './profile-card.html',
  styleUrl: './profile-card.css'
})
export class ProfileCard implements OnInit{
  userDetails?:any;
  constructor(private _userData:UserDataStore){}

  ngOnInit(): void {
    // Current user details
    this._userData.user$.subscribe(user => {      
      if(!user) return;
      this.userDetails = user;
    });    
  }
}
