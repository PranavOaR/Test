import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
import Home from '../app/page';

describe('Home', () => {
    it('renders heading', () => {
        render(<Home />);
        const heading = screen.getByText(/Football League/i);
        expect(heading).toBeInTheDocument();
    });
});
