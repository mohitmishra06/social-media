import { CommonModule } from '@angular/common';
import { Component, Input, OnInit } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faBook, faImage, faMessage, faPeopleGroup, faUsers, faVideo } from '@fortawesome/free-solid-svg-icons';
import { ProfileCard } from '../../profile/leftmenu/profile-card/profile-card';
import { Ad } from "../rightmenu/ad/ad";
import { People } from "./people/people";

@Component({
  selector: 'app-leftmenu',
  imports: [CommonModule, FontAwesomeModule, ProfileCard, Ad, People],
  templateUrl: './leftmenu.html',
  styleUrl: './leftmenu.css'
})
export class Leftmenu{
  @Input() type?:string;
  icon = { faBook, faImage, faMessage, faPeopleGroup, faVideo, faUsers, }

}
