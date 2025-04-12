import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MailViewerDialogComponent } from './mail-viewer-dialog.component';

describe('MailViewerDialogComponent', () => {
  let component: MailViewerDialogComponent;
  let fixture: ComponentFixture<MailViewerDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MailViewerDialogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MailViewerDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
