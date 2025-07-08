import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-user-information-card',
  imports: [],
  templateUrl: './user-information-card.html',
  styleUrl: './user-information-card.css'
})
export class UserInformationCard {
  @Input() userId?:string
}
