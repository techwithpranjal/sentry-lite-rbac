import { CanActivateChildFn, Router } from '@angular/router';


export const testGuard: CanActivateChildFn = () => {
    alert('GUARD RAN');
    return false;
  };