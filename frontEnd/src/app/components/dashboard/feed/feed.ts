import { Component } from '@angular/core';
import { Post } from "../post/post";

@Component({
  selector: 'app-feed',
  imports: [Post],
  templateUrl: './feed.html',
  styleUrl: './feed.css'
})
export class Feed {

}
