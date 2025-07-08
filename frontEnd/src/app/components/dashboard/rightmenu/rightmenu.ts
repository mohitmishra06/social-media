import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { Ad } from "./ad/ad";
import { FriendRequests } from "./friend-requests/friend-requests";
import { Birthdays } from "./birthdays/birthdays";
import { AcceptedFriends } from "./accepted-friends/accepted-friends";
import { UserInformationCard } from "../../profile/user-information-card/user-information-card";
import { UserMediaCard } from "../../profile/user-media-card/user-media-card";

@Component({
  selector: 'app-rightmenu',
  imports: [CommonModule, Ad, FriendRequests, Birthdays, AcceptedFriends, UserInformationCard, UserMediaCard],
  templateUrl: './rightmenu.html',
  styleUrl: './rightmenu.css'
})
export class Rightmenu {
  @Input() userId?:string;
}
