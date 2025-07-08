import { Component } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faThumbsUp } from '@fortawesome/free-solid-svg-icons';
import { Leftmenu } from "../../components/dashboard/leftmenu/leftmenu";
import { Feed } from "../../components/dashboard/feed/feed";
import { Rightmenu } from "../../components/dashboard/rightmenu/rightmenu";

@Component({
  selector: 'app-profile',
  imports: [FontAwesomeModule, Leftmenu, Feed, Rightmenu],
  templateUrl: './profile.html',
  styleUrl: './profile.css'
})
export class Profile {
  icon = { faThumbsUp }
}
