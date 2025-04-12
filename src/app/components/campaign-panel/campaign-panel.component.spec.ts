import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CampaignPanelComponent } from './campaign-panel.component';

describe('CampaignPanelComponent', () => {
  let component: CampaignPanelComponent;
  let fixture: ComponentFixture<CampaignPanelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CampaignPanelComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CampaignPanelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
