import { Component, OnInit } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faThumbsUp } from '@fortawesome/free-solid-svg-icons';
import { Leftmenu } from "../../components/dashboard/leftmenu/leftmenu";
import { Feed } from "../../components/dashboard/feed/feed";
import { Rightmenu } from "../../components/dashboard/rightmenu/rightmenu";
import { UserDataStore } from '../../services/userData/user-data-store';

@Component({
  selector: 'app-profile',
  imports: [FontAwesomeModule, Leftmenu, Feed, Rightmenu],
  templateUrl: './profile.html',
  styleUrl: './profile.css'
})
export class Profile implements OnInit{
  icon = { faThumbsUp }
  userDetails:any;
  
  constructor(private _userData:UserDataStore){}

  ngOnInit(): void {
    this._userData.glbUserData.subscribe(val=>{
      this.userDetails = val
    })
  }
}
