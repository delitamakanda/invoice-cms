const filters = {
    currency(value) {
      if (isNaN(value)) {
        return "-";
      }
      return `${value.toFixed(2)}€`;
    },
    decimal(value) {
      if (isNaN(value)) {
        return 0;
      }
      return value.toFixed(2);
    }
}

export default filters;