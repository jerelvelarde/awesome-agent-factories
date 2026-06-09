import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import React from "react";
import { ApprovalCard } from "../src/ApprovalCard";

describe("ApprovalCard (human-in-the-loop gate)", () => {
  it("renders an approve control for the gated tool", () => {
    // RED until ApprovalCard is implemented.
    render(<ApprovalCard toolName="open_pr" onApprove={vi.fn()} onDeny={vi.fn()} />);
    expect(screen.getByRole("button", { name: /approve/i })).toBeTruthy();
  });
});
