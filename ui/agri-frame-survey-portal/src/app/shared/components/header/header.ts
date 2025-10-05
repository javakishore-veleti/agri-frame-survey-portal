import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { NgClass } from '@angular/common';
import { NavService } from '@shared/components/navigation/nav.service';
import { AuthService } from '@core/services/auth.service';

@Component({
  selector: 'af-header',
  standalone: true,
  imports: [RouterLink, RouterLinkActive, NgClass],
  templateUrl: './header.html',
})
export class HeaderComponent {
  nav = inject(NavService);
  auth = inject(AuthService);
}
