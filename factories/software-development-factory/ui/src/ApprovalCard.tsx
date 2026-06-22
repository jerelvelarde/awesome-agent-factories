import React from "react";

export interface ApprovalCardProps {
  /** The approval-gated tool awaiting confirmation, e.g. "open_pr". */
  toolName: string;
  onApprove: () => void;
  onDeny: () => void;
}

/**
 * Renders the human-in-the-loop approval step for a gated tool interrupt.
 *
 * Not implemented yet (red scaffold) — should render an Approve and a Deny
 * control wired to the deep agent's interrupt.
 */
export function ApprovalCard(_props: ApprovalCardProps): React.ReactElement {
  throw new Error("ApprovalCard is not implemented yet (red scaffold)");
}
