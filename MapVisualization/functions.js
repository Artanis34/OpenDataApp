export function getColorFromStatus(status) {
    switch (status) {
        case 1: return 'red';
        case 2: return 'orange';
        case 3: return 'green';
        default: return 'gray';
    }
}