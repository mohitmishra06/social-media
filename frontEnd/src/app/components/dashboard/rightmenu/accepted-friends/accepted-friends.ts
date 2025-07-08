import { Component } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faChevronRight } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-accepted-friends',
  imports: [FontAwesomeModule],
  templateUrl: './accepted-friends.html',
  styleUrl: './accepted-friends.css'
})
export class AcceptedFriends {
  icon={faChevronRight}
}
