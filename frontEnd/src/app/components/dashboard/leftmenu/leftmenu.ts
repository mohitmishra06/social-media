import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faBook, faImage, faMessage, faPeopleGroup, faUsers, faVideo } from '@fortawesome/free-solid-svg-icons';
import { ProfileCard } from '../../profile/leftmenu/profile-card/profile-card';
import { Ad } from "../rightmenu/ad/ad";

@Component({
  selector: 'app-leftmenu',
  imports: [CommonModule, FontAwesomeModule, ProfileCard, Ad],
  templateUrl: './leftmenu.html',
  styleUrl: './leftmenu.css'
})
export class Leftmenu {
  @Input() type?:string;
  icon = { faBook, faImage, faMessage, faPeopleGroup, faVideo, faUsers, }
}
