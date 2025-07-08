import { Component } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faComment, faShare, faThumbsUp } from '@fortawesome/free-solid-svg-icons';
import { Comments } from "./comments/comments";

@Component({
  selector: 'app-post',
  imports: [FontAwesomeModule, Comments],
  templateUrl: './post.html',
  styleUrl: './post.css'
})
export class Post {
  icon={faThumbsUp, faComment, faShare}
}
