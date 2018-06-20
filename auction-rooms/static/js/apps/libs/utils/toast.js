export const successToast = msg => (
  Materialize.toast(
    `<span><i class="material-icons left">check_circle</i>${msg}</span>`,
    4000,
    'success'
  )
);

export const warningToast = msg => (
  Materialize.toast(
    `<span><i class="material-icons left">warning</i>${msg}</span>`,
    4000,
    'warning'
  )
);

export const errorToast = msg => (
  Materialize.toast(
    `<span><i class="material-icons left">error</i>${msg}</span>`,
    4000,
    'error'
  )
);

export const infoToast = msg => (
  Materialize.toast(
    `<span><i class="material-icons left">info</i>${msg}</span>`,
    4000,
    'info'
  )
);
