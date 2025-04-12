import {Component, OnDestroy, OnInit} from '@angular/core';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatIconModule} from '@angular/material/icon';
import {Subscription} from 'rxjs';
import {HttpService} from '../../services/http.service';
import {WebpageMetrics} from '../../data/metrics.data';

@Component({
  selector: 'app-analytics-panel',
  imports: [MatExpansionModule, MatIconModule],
  templateUrl: './analytics-panel.component.html',
  styleUrl: './analytics-panel.component.css'
})
export class AnalyticsPanelComponent implements OnInit, OnDestroy {

  private subscriptions: Subscription[] = [];
  public metrics: WebpageMetrics = {clicks: 0, mailsSent: 0, openedMails: 0, clickedMails: 0, purchases: 0, avgPurchaseTime: 0};
  public conversionRate: number = 0;


  constructor(private httpService: HttpService) {}

  public ngOnInit() {
    this.subscriptions.push(this.httpService.getWebpageMetrics()
      .subscribe(metrics => {
        this.metrics = metrics;
        this.conversionRate = metrics.clicks > 0 ? metrics.purchases / metrics.clicks : 0;
      }));
  }

  public ngOnDestroy() {
    this.subscriptions.forEach(s => s.unsubscribe());
  }

}
