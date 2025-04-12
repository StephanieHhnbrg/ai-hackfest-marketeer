import { Component } from '@angular/core';
import {ToolbarComponent} from './components/toolbar/toolbar.component';
import {CampaignPanelComponent} from './components/campaign-panel/campaign-panel.component';
import {AnalyticsPanelComponent} from './components/analytics-panel/analytics-panel.component';
import {EventPanelComponent} from './components/event-panel/event-panel.component';

@Component({
  selector: 'app-root',
  imports: [ToolbarComponent, CampaignPanelComponent, EventPanelComponent, AnalyticsPanelComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
}
