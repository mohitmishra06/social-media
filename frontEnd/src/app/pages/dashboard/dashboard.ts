import { Component } from '@angular/core';
import { Leftmenu } from "../../components/dashboard/leftmenu/leftmenu";
import { Rightmenu } from "../../components/dashboard/rightmenu/rightmenu";
import { Stories } from "../../components/dashboard/stories/stories";
import { Addpost } from "../../components/dashboard/addpost/addpost";
import { Feed } from "../../components/dashboard/feed/feed";

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
  imports: [Leftmenu, Rightmenu, Stories, Addpost, Feed]
})
export class Dashboard {
}
