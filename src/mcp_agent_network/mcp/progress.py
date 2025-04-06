"""Progress indicators for MCP operations."""

import sys
import time
from typing import Optional


class ProgressBar:
    """Simple progress bar for command-line interfaces.
    
    Displays a progress bar with percentage and status message.
    """
    
    def __init__(self, total: int, description: str = "Progress", width: int = 40):
        """Initialize the progress bar.
        
        Args:
            total: Total number of steps
            description: Description of the operation
            width: Width of the progress bar in characters
        """
        self.total = total
        self.description = description
        self.width = width
        self.current = 0
        self.start_time = time.time()
        self.status = ""
        
    def update(self, current: int, status: Optional[str] = None) -> None:
        """Update the progress bar.
        
        Args:
            current: Current step
            status: Optional status message
        """
        self.current = current
        if status:
            self.status = status
        
        self._render()
        
    def finish(self) -> None:
        """Mark the progress as complete."""
        self.update(self.total, "Complete")
        sys.stdout.write("\n")
        sys.stdout.flush()
        
    def _render(self) -> None:
        """Render the progress bar."""
        percent = self.current / self.total
        filled_width = int(self.width * percent)
        bar = "█" * filled_width + "░" * (self.width - filled_width)
        
        elapsed = time.time() - self.start_time
        if percent > 0:
            eta = elapsed / percent - elapsed
            eta_str = f"ETA: {eta:.1f}s"
        else:
            eta_str = "ETA: --"
            
        # Format: [Description] [Progress Bar] xx% Status | Elapsed: xx.xs | ETA: xx.xs
        output = f"\r{self.description}: [{bar}] {percent*100:.1f}% | {self.status} | Elapsed: {elapsed:.1f}s | {eta_str}"
        
        # Truncate if too long for terminal
        term_width = 80  # Assume default terminal width
        if len(output) > term_width:
            output = output[:term_width-3] + "..."
            
        sys.stdout.write(output)
        sys.stdout.flush()


class SpinnerIndicator:
    """Spinner indicator for processes without known progress.
    
    Displays a spinning cursor to indicate activity.
    """
    
    def __init__(self, description: str = "Processing"):
        """Initialize the spinner.
        
        Args:
            description: Description of the operation
        """
        self.description = description
        self.frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.current_frame = 0
        self.start_time = 0
        self.running = False
        self.status = ""
        
    def start(self, status: Optional[str] = None) -> None:
        """Start the spinner.
        
        Args:
            status: Optional status message
        """
        self.running = True
        self.start_time = time.time()
        if status:
            self.status = status
        
    def update(self, status: str) -> None:
        """Update the spinner status.
        
        Args:
            status: New status message
        """
        self.status = status
        self._render()
        
    def stop(self) -> None:
        """Stop the spinner."""
        self.running = False
        sys.stdout.write("\r")
        sys.stdout.flush()
        
    def _render(self) -> None:
        """Render the spinner."""
        if not self.running:
            return
        
        frame = self.frames[self.current_frame]
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        
        elapsed = time.time() - self.start_time
        
        output = f"\r{frame} {self.description}: {self.status} | Elapsed: {elapsed:.1f}s"
        
        # Truncate if too long for terminal
        term_width = 80  # Assume default terminal width
        if len(output) > term_width:
            output = output[:term_width-3] + "..."
            
        sys.stdout.write(output)
        sys.stdout.flush() 